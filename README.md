
### **Image Steganography Application**

![GitHub](https://img.shields.io/badge/Python-3.x-blue) ![License](https://img.shields.io/badge/License-MIT-green)

A user-friendly desktop application to embed secret messages into images using steganography techniques. Built with Python's `tkinter` for the GUI and OpenCV (`cv2`) for image manipulation, this tool ensures secure and covert communication.

---

## **Overview**

This application allows users to encode secret messages into images and decode them back securely. It uses the **Least Significant Bit (LSB)** technique to hide messages within the pixel data of an image. The application also provides a password field (currently unused) that can be extended for encryption purposes in the future.

Perfect for privacy-conscious individuals, cybersecurity enthusiasts, or anyone interested in experimenting with steganography!

---

## **Features**

- **Encode Messages**: Embed text messages into images without noticeable distortion.
- **Decode Messages**: Extract hidden messages from encoded images.
- **Password Field**: Placeholder for future integration of password-based encryption.
- **Text File Support**: Load secret messages directly from `.txt` files.
- **Error Handling**: Prevents encoding if the message exceeds the image's capacity.
- **User-Friendly GUI**: Intuitive interface built with `tkinter` for ease of use.
- **Dynamic Message Length**: Stores the message length in the first pixel for efficient decoding.
- **Cross-Platform**: Works on Windows, macOS, and Linux.

---

## **Technologies Used**

- **Python**: Core programming language.
- **Tkinter**: GUI toolkit for creating the user interface.
- **OpenCV (`cv2`)**: Library for image processing and manipulation.
- **File Handling**: For loading text files and saving encoded images.
- **Error Handling**: Ensures robustness against invalid inputs or corrupted images.

---

## **Installation**

### **Prerequisites**

- Python 3.x installed on your system.
- Required libraries: `opencv-python`, `tkinter`.

### **Steps**

1. Clone the repository:
   ```bash
   git clone https://github.com/Gowtham-911/image-steganography.git
   cd image-steganography
   ```

2. Install dependencies:
   ```bash
   pip install opencv-python
   ```

3. Run the application:
   ```bash
   python main.py
   ```

---

## **Usage**

1. **Encoding a Message**:
   - Select an image file (`.jpg`, `.png`, `.bmp`).
   - Enter or load a secret message into the text box.
   - Provide a password (optional for now).
   - Click "Encode Message" to generate the encoded image.

2. **Decoding a Message**:
   - Select the encoded image.
   - Enter the password (if applicable).
   - Click "Decode Message" to extract the hidden text.

---


## **Future Improvements**

- **Password-Based Encryption**: Use the password field to encrypt/decrypt messages before embedding/extraction.
- **Support for Other Formats**: Extend functionality to handle additional file types (e.g., audio, video).
- **Advanced Encoding Techniques**: Implement more sophisticated steganography methods (e.g., adaptive LSB, spread spectrum).
- **Batch Processing**: Allow encoding/decoding multiple images at once.
- **Steganalysis Detection**: Add tools to detect steganography in images.

---

## **Contributing**

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m "Add YourFeatureName"`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a pull request.

For major changes, please open an issue first to discuss what you'd like to add or improve.

---

## **License**

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

