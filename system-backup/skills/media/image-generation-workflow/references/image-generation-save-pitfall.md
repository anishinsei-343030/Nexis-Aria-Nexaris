# Saving Image Generation Output Pitfall

## Issue Description
When using image generation tools like `image_gen` or `apikey-image-gen`, directly piping the tool's output to `write_file` or attempting to save the generated image using text-based file writing methods will result in failure or corrupted image files. The `write_file` tool is specifically designed for text content and cannot correctly handle binary image data.

## Reproduction Steps
1. Attempt to generate an image using `image_gen` or `apikey-image-gen`.
2. Try to capture the output of the image generation tool and pass it as `content` to `write_file`.

   ```bash
   # This will fail or create a corrupted file
   write_file path="my_image.png" content="$(image_gen --provider stability_ai --prompt "a beautiful landscape")"
   ```

## Root Cause
Image generation tools return binary data (e.g., PNG, JPEG). The `write_file` tool processes its `content` argument as a string, expecting text data. When binary data is forced into a string context, it becomes corrupted or causes encoding errors, preventing proper file saving.

## Solution
Always use the dedicated `--output` (or equivalent) parameter within the image generation tool call itself to specify the output file path. This allows the tool to handle the binary stream correctly and save the image directly to disk.

```bash
# Correct approach: Output path specified directly in image_gen
image_gen --provider stability_ai --prompt "a beautiful landscape" --output "my_image.png"
```

This ensures that the image is saved as a proper binary file without corruption.
