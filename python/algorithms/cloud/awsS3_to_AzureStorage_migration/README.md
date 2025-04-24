
# 📂 S3 to Azure Blob Storage Migration Script

This Python script allows you to **migrate files from an AWS S3 bucket to an Azure Blob Storage container**.  
It uses a `.env` file to securely store your AWS and Azure credentials.

---

## 🚀 Features

- ✅ Download files from AWS S3
- ✅ Upload files to Azure Blob Storage
- ✅ Supports folder structures
- ✅ Simple `.env` configuration for credentials

---

## 📁 Project Structure

```
your-folder/
├── s3_to_azure.py            # Main migration script
├── .env                      # Environment variables (not committed)
├── requirements.txt          # Python dependencies
├── README.md                 # Documentation
└── venv/                     # Virtual environment (optional but recommended)
```

---

## 🛠️ Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2️⃣ Create Your `.env` File

Create a `.env` file in the project root with the following content:

```dotenv
# AWS S3 Settings
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_aws_region
AWS_BUCKET_NAME=your_s3_bucket_name

# Azure Blob Storage Settings
AZURE_STORAGE_CONNECTION_STRING=your_azure_storage_connection_string
AZURE_CONTAINER_NAME=your_azure_container_name
```

> ⚠️ **Keep the `.env` file private and never commit it to version control.**

---

## 💾 Install Dependencies

### Using Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

If `requirements.txt` is not available, manually install:

```bash
pip install boto3 azure-storage-blob python-dotenv
```

---

## ▶️ How to Run

Make sure your virtual environment is active:

```bash
source venv/bin/activate
python s3_to_azure.py
```

---

## 📂 How It Works

1. Downloads files from the specified **AWS S3 bucket**.
2. Saves the files temporarily in the `s3_download_temp/` directory.
3. Uploads the downloaded files to the specified **Azure Blob Storage container**.
4. Overwrites existing blobs in Azure if the filenames match.

---

## 🟢 Example Output

```
Downloading files from S3...
Downloading example/file1.txt to s3_download_temp/example/file1.txt
Uploading s3_download_temp/example/file1.txt as example/file1.txt
Migration completed successfully.
```

---

## 📌 Notes

- The script performs a **one-time migration** of all files from S3 to Azure Blob.
- Temporary files are stored in the `s3_download_temp/` folder.
- Remember to clean up the local temporary folder after migration if needed.
- Currently, the script does not handle incremental sync (future enhancement possible).

---

## 🛡️ License

MIT License.  
Feel free to use, modify, and share.