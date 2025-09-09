#include<iostream>
#include <iomanip>
#include <cstdint>
#include <cstring>
#include <ctime>
#include <fstream>
#include <vector>
using namespace std;

// bool logs = false; // toggle on/off for detailed logs

#define ROTL32(x, n) ((x << n) | (x >> (32 - n)))

#define quarterRound(y0, y1, y2, y3) \
    y0 += y1; y3 ^=y0; y3 = ROTL32(y3, 16); \
    y2 += y3; y1 ^=y2; y1 = ROTL32(y1, 12); \
    y0 += y1; y3 ^=y0; y3 = ROTL32(y3, 8); \
    y2 += y3; y1 ^=y2; y1 = ROTL32(y1, 7);

#define diagonalRound(y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15) \
    quarterRound(y0, y5, y10, y15); \
    quarterRound(y1, y6, y11, y12); \
    quarterRound(y2, y7, y8, y13); \
    quarterRound(y3, y4, y9, y14);

#define columnRound(y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15) \
    quarterRound(y0, y4, y8, y12); \
    quarterRound(y1, y5, y9, y13); \
    quarterRound(y2, y6, y10, y14); \
    quarterRound(y3, y7, y11, y15);

#define doubleRound(y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15) \
    columnRound(y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15); \
    diagonalRound(y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15);
    

uint32_t littleendian(const uint32_t b[4]) {
    return ((uint32_t)b[0]) |
           ((uint32_t)b[1] << 8) |
           ((uint32_t)b[2] << 16) |
           ((uint32_t)b[3] << 24);
}
static void store_littleendian(uint32_t *x, uint32_t u) {
    x[0] = u & 0xff;
    x[1] = (u >> 8) & 0xff;
    x[2] = (u >> 16) & 0xff;
    x[3] = (u >> 24) & 0xff;
}
static uint32_t load_littleendian(const uint32_t *x) {
    return ((uint32_t)x[0])       |
           ((uint32_t)x[1] << 8)  |
           ((uint32_t)x[2] << 16) |
           ((uint32_t)x[3] << 24);
}

void printchachaState(const uint32_t output[16]) {
    for (int row = 0; row < 4; row++) {
        for (int col = 0; col < 4; col++) {
            int idx = row * 4 + col;
            cout << "0x"
                 << setw(8) << setfill('0') << hex << nouppercase
                 << output[idx] << " ";
        }
        cout << endl;
    }
    cout << dec; // reset to decimal mode
}

uint32_t* chacha20Core(uint32_t input[16], bool logs) {
    uint32_t* output = new uint32_t[16];
    for (int i = 0; i < 16; i++) {
        output[i] = input[i];
    }
    for (int i = 0; i<10; i++){
        
        columnRound(
            output[0], output[1], output[2], output[3],
            output[4], output[5], output[6], output[7],
            output[8], output[9], output[10], output[11],
            output[12], output[13], output[14], output[15]
        );
        if(logs){
            cout << endl << "Column Round " << i+1 << ": " << endl;
            printchachaState(output);
        }
        
        
        diagonalRound(
            output[0], output[1], output[2], output[3],
            output[4], output[5], output[6], output[7],
            output[8], output[9], output[10], output[11],
            output[12], output[13], output[14], output[15]
        );
        if(logs){
            cout << endl << "Diagonal Round " << i+1 << ": " << endl;
            printchachaState(output);
        }
        
    }
    return output;
}

uint32_t* chacha20(uint32_t* key, uint32_t* nonce, uint64_t counter, bool logs){

uint32_t constant[16] = {'e', 'x', 'p', 'a', 'n', 'd', ' ', '3', '2', '-', 'b', 'y', 't', 'e', ' ', 'k'};

    uint32_t counter_bytes[4];
    store_littleendian(counter_bytes, (uint32_t)(counter & 0xFFFFFFFF));


    /*
        c0, c1, c2, c3,
        k0, k1, k2, k3,
        k4, k5, k6, k7,
        t0, v1, v2, v3
    */
    uint32_t input[16];
    input[0]  = littleendian(&constant[0]);
    input[1]  = littleendian(&constant[4]);
    input[2]  = littleendian(&constant[8]);
    input[3]  = littleendian(&constant[12]);
    input[4]  = key[0];
    input[5]  = key[1];
    input[6]  = key[2];
    input[7]  = key[3];
    input[8]  = key[4];
    input[9]  = key[5];
    input[10] = key[6];
    input[11] = key[7];
    input[12] = load_littleendian(counter_bytes);
    input[13] = littleendian(&nonce[0]);
    input[14] = littleendian(&nonce[4]);
    input[15] = littleendian(&nonce[8]);
    
    if(logs){
        cout<<endl<<"Initial State:"<<endl;
        printchachaState(input);
    }

    
    uint32_t* output = chacha20Core(input, logs);

    uint32_t* keyStream = new uint32_t[16];
    for (int i = 0; i < 16; i++) {
        keyStream[i] = output[i] + input[i];
    }
    if (logs){
        cout<<endl<< "Keystream: " << endl;
        printchachaState(keyStream);
    }
    
    
   uint32_t* keystream_bytes = new uint32_t[64];
    for (int i = 0; i < 16; i++) {
        keystream_bytes[i*4 + 0] = (output[i] + input[i]) & 0xFF;
        keystream_bytes[i*4 + 1] = ((output[i] + input[i]) >> 8) & 0xFF;
        keystream_bytes[i*4 + 2] = ((output[i] + input[i]) >> 16) & 0xFF;
        keystream_bytes[i*4 + 3] = ((output[i] + input[i]) >> 24) & 0xFF;
    }
    return keystream_bytes;
};
vector<uint8_t> chacha20_block_encrypt(vector<uint8_t> plaintext, const uint32_t* keystream) {
    vector<uint8_t> ciphertext(64);
    for (size_t i = 0; i < 64; i++) {
        ciphertext[i] = plaintext[i] ^ keystream[i];
    }
    return ciphertext;
}

// Print as hex dump
void display_hex(const vector<uint8_t> &text) {
    for (size_t i = 0; i < text.size(); i++) {
        cout << hex << setw(2) << setfill('0') << (int)text[i] << " ";
        if ((i + 1) % 16 == 0) cout << "\n";
    }
    cout << dec << endl; // reset to decimal
}

// Print as ASCII text (non-printables replaced with '.')
void display_text(const vector<uint8_t> &text) {
    for (auto b : text) {
        if (isprint(b)) cout << (char)b;
        else cout << ".";
    }
    cout << endl;
}

// Helper to read entire file into buffer
vector<uint8_t> readFile(const string &filename) {
    ifstream file(filename, ios::binary);
    if (!file) {
        throw runtime_error("Error opening file: " + filename);
    }
    return vector<uint8_t>((istreambuf_iterator<char>(file)), istreambuf_iterator<char>());
}

// Split buffer into 512-bit (64-byte) blocks
vector<vector<uint8_t>> splitBlocks(const vector<uint8_t> &data, size_t blockSize = 64) {
    vector<vector<uint8_t>> blocks;
    size_t total = data.size();

    for (size_t i = 0; i < total; i += blockSize) {
        vector<uint8_t> block(blockSize, 0); // pad with zeros if not full
        size_t len = min(blockSize, total - i);
        copy(data.begin() + i, data.begin() + i + len, block.begin());
        blocks.push_back(block);
    }
    return blocks;
}

// Print block (for debug)
void printBlock(const vector<uint8_t> &block) {
    for (size_t i = 0; i < block.size(); i++) {
        cout  << (int)block[i] << " ";
        if ((i + 1) % 16 == 0) cout << endl;
    }
    cout << endl;
}

void writeFile(const string &filename, const vector<uint8_t> &data) {
    ofstream file(filename, ios::binary);
    if (!file) {
        throw runtime_error("Error writing file: " + filename);
    }
    file.write(reinterpret_cast<const char*>(data.data()), data.size());
}

void diffusion(uint32_t* key, uint32_t* nonce, bool logs){
    //Block to check the diffusion rounds starts
    string text = "Hey I am Arnav. Roll: CS24M801";
    vector<uint8_t> plaintext(text.begin(), text.end());
    vector<uint64_t> counter = {0, 1, 801, 802}; // Set counter Values 0, 1, 801, 802
    for (uint32_t c : counter) {
        if(logs){
            cout<<endl<<"Key: ";
            for(int i =0;i<32;i++){
                cout<<key[i];
            }
            cout<<endl;

            cout<<endl<<"Nonce: ";
            for(int i =0;i<12;i++){
                cout<<nonce[i];
            }
            cout<<endl;
            cout<<endl<<"Counter: "<<c<<endl;
        }
        clock_t start = clock();
        uint32_t* ks = chacha20(key, nonce, c, logs);
        clock_t end = clock();
        double cpu_time = 1000.0 * (end - start) / CLOCKS_PER_SEC;
        vector<uint8_t> ciphertext = chacha20_block_encrypt(plaintext, ks);
        ciphertext.resize(plaintext.size()); // resize to original plaintext size
        vector<uint8_t> decrypttext = chacha20_block_encrypt(ciphertext, ks);
        decrypttext.resize(plaintext.size()); // resize to original plaintext size
        if(logs){
            cout<<endl<<"plaintext(Text): "<<endl;
            display_text(plaintext);
            cout<<endl<<"Plaintext (Hex): "<<endl;
            display_hex(plaintext);
            cout<<endl<<"Ciphertext(Text): "<<endl;
            display_text(ciphertext);
            cout<<endl<<"Ciphertext (Hex): "<<endl;
            display_hex(ciphertext);
            cout<<endl<<"Decrypted (Text): "<<endl;
            display_text(decrypttext);
            cout<<endl<<"Decrypted (Hex): "<<endl;
            display_hex(decrypttext);
        }
        cout<<endl<< "chacha 20 execution Time: " << cpu_time << "ms" << endl;
    }
    // Block to check the diffusion rounds ends
}

void encrypt_decrypt_file(uint32_t* key, uint32_t* nonce, string inputFileName, string outputFileName, bool logs){
    //Block to encrypt/decrypt a file starts
    string originalFileName = inputFileName; // Donot Change ["CS24M801_CS6530_Assgn1_Part1.txt"]

    // string inputFileName = "CS24M801_CS6530_Assgn1_Part1_Encrypted.bin"; // Replace with your input file path  ["CS24M801_CS6530_Assgn1_Part1.txt" | "CS24M801_CS6530_Assgn1_Part1_Encrypted.bin"]
    // string outputFileName = "CS24M801_CS6530_Assgn1_Part1_Decrypted.bin"; //Replace with yout output file path ["CS24M801_CS6530_Assgn1_Part1_Encrypted.bin" | "CS24M801_CS6530_Assgn1_Part1_Decrypted.bin"]

    //Reading File
    vector<uint8_t> originalFileData = readFile(originalFileName);
    size_t originalSize = originalFileData.size();
    vector<uint8_t> fileData = readFile(inputFileName);
    cout << "File size: " << fileData.size() << " bytes" << endl;
    // Break into 64-byte (512-bit) blocks
    vector<vector<uint8_t>> blocks = splitBlocks(fileData);
    cout << "Total blocks: " << blocks.size() << endl;
    vector<uint8_t> plaintext;
    vector<uint8_t> ciphertext;
    uint64_t counter = 0;

    plaintext.reserve(fileData.size());
    ciphertext.reserve(fileData.size());
    clock_t start = clock();

    for (size_t i = 0; i <  blocks.size(); i++) {
        if(logs){
            cout<<endl<<"Key: ";
            for(int i =0;i<32;i++){
                cout<<key[i];
            }
            cout<<endl;

            cout<<endl<<"Nonce: ";
            for(int i =0;i<12;i++){
                cout<<nonce[i];
            }
            cout<<endl;
            cout<<endl<<"Counter: "<<counter + i<<endl;
        }
        uint32_t* ks = chacha20(key, nonce, counter + i, logs); // get keystream for this block
        vector<uint8_t> ctBlock = chacha20_block_encrypt(blocks[i], ks);

        // Append ciphertext block
        ciphertext.insert(ciphertext.end(), ctBlock.begin(), ctBlock.end());
        plaintext.insert(plaintext.end(), blocks[i].begin(), blocks[i].end());
    }
    if(logs){
        cout<<endl<<"Plaintext: "<<endl;
        display_text(plaintext);
        cout<<endl<<"Ciphertext: "<<endl;
        display_text(ciphertext);
    }

    clock_t end = clock();
    // 🔹 Remove padded bytes
    ciphertext.resize(originalSize);
    writeFile(outputFileName, ciphertext);
    cout << "Ciphertext written to "<< outputFileName << endl;

    double cpu_time = 1000.0 * (end - start) / CLOCKS_PER_SEC;
    cout<<endl<< "chacha 20 execution Time: " << cpu_time << "ms" << endl;
    //Block to encrpyt/decrpyt the file ends

}
int main(int argc, char* argv[]) {
    if (argc != 5) {
        cerr << "Usage: " << argv[0] << " <keyfile (32 bytes)> <nonce size ignored, fixed zero nonce used> <input_zip> <output_encrypted>" << endl;
        return 1;
    }

    string keyfile = argv[1];
    string inputfile = argv[2];
    string outputfile = argv[3];
    bool logs = argv[4] == string("true") ? true : false;

    try {
        // Read symmetric key from file (must be exactly 32 bytes)
        vector<uint8_t> keyBytes = readFile(keyfile);
        if (keyBytes.size() != 32) {
            cerr << "Error: Key file must be exactly 32 bytes (256 bits)" << endl;
            return 2;
        }
        // Parse keyBytes safely into 8 little-endian 32-bit words
        uint32_t key[8];
        for (int i = 0; i < 8; i++) {
            key[i] = ((uint32_t)keyBytes[i*4 + 0]) |
                     ((uint32_t)keyBytes[i*4 + 1] << 8)  |
                     ((uint32_t)keyBytes[i*4 + 2] << 16) |
                     ((uint32_t)keyBytes[i*4 + 3] << 24);
        }
        // Display key
        if(logs){
            cout << "Key (hex): ";
            for (auto b : keyBytes) {
                cout << hex << setw(2) << setfill('0') << (int)b;
            }
            cout << dec << endl; // reset to decimal
        }

        // Fixed zero nonce
        uint32_t nonce[12] = {0};

        // Call your encrypt_decrypt_file function
        // Parameters: key, nonce, inputFilePath, outputFilePath, logs_on (true here)
        encrypt_decrypt_file(key, nonce, inputfile, outputfile, logs);

//        cout << "Encryption successful." << endl;
//        cout << "Input: " << inputfile << endl;
        cout << "Output: " << outputfile << endl;

    } catch (const exception &ex) {
        cerr << "Exception: " << ex.what() << endl;
        return 3;
    }

    return 0;
}
