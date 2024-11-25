export const convertImageToBase64 = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => {
            if (typeof reader.result === 'string') {
                resolve(reader.result); // Return Base64 string
            } else {
                reject(new Error('FileReader result is not a string.'));
            }
        };
        reader.onerror = (error) => {
            reject(error); // Handle error
        };
        reader.readAsDataURL(file); // Read file as data URL
    });
};

export const decodeBase64ToBlob = (base64: string): Blob => {
    const arr = base64.split(',');
    const mime = arr[0].match(/:(.*?);/)?.[1]; // Get MIME type
    const bstr = atob(arr[1]); // Decode Base64 string
    const n = bstr.length;
    const u8arr = new Uint8Array(n);

    for (let i = 0; i < n; i++) {
        u8arr[i] = bstr.charCodeAt(i); // Convert to byte array
    }

    return new Blob([u8arr], { type: mime }); // Create Blob from byte array
};
