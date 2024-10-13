python python-clients/scripts/asr/transcribe_file.py \
    --server grpc.nvcf.nvidia.com:443 --use-ssl \
    --metadata function-id "d8dd4e9b-fbf5-4fb0-9dba-8cf436c8d965" \
    --metadata "authorization" "Bearer $API_KEY_REQUIRED_IF_EXECUTING_OUTSIDE_NGC" \
    --language-code en-US \
    --input-file <path_to_audio_file>