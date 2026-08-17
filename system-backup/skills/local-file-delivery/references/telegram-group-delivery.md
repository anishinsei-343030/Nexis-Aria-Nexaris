# Telegram Group Chat File Delivery

## Error Encountered

When attempting to deliver files to a Telegram group chat using `send_message` with `MEDIA:` tags, the following error may occur:

```
"No deliverable text or media"
```

This error indicates that the `MEDIA:` tag was not processed correctly for the group chat.

## Workaround

1. **Confirm File Path**: Verify the file exists and the path is absolute.
2. **Split Large Files**: Use `split` to divide files larger than 2 GB:
   ```bash
   split -b 1900M "input_file" "output_prefix_"
   ```
3. **Retry with Explicit Text**: Include a text message alongside the `MEDIA:` tag:
   ```
   send_message(target="telegram:<chat_id>:<thread_id>", message="MEDIA:<file_path>")
   ```
4. **Verify Delivery**: Check the output of `send_message` to confirm success.

## Example

```bash
# Split a large file
split -b 1900M "/c/Users/Administrator/Documents/Gerald T. Cortez Resume.docx" "Gerald_Resume_Part_"

# Send each part
send_message(target="telegram:-1003740504045", message="MEDIA:/c/Users/Administrator/Gerald_Resume_Part_aa")
send_message(target="telegram:-1003740504045", message="MEDIA:/c/Users/Administrator/Gerald_Resume_Part_ab")
```