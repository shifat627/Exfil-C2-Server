# Exfil-C2-Server
I made this server to recieve files over internet


You can fetch file from
**/s/<fileName>** for static files
**/files/<uploadedFileName>** for uploaded file


Upload File:
**/give** have **File** parameter.USE POST METHOD
**/giveRaw/<filename>** for RAW body.Meaning it will put content of body in a fil**e
/multiple_upload_Files** have **File** parameter.this is for multiple files
