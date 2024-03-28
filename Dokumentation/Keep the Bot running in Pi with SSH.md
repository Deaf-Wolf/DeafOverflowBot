#### Introduction

When running a Discord bot on a Raspberry Pi through SSH, it's crucial to ensure that the bot continues running even after closing the SSH connection. Here's a step-by-step guide:

#### Step 1: Navigate to the Bot Directory

```bash
cd /path/to/your/bot/directory
```

Replace `/path/to/your/bot/directory` with the actual path to your Discord bot's directory.

#### Step 2: Run the Bot with `nohup`

```bash
nohup python3 main.py &
```

This command uses `nohup` to run the Python script (`main.py`) in the background and detaches it from the terminal. The `&` symbol ensures that the process continues running even after the SSH connection is closed.

#### Step 3: Verify the Process

To check if the bot process is running:

```bash
ps aux | grep python3
```

Look for the line related to your `main.py` script. The output will show the process ID (PID) and other information.

```bash
ps -p <PID>
```

Replace `<PID>` with the actual process ID to get more detailed information about the specific process.

#### Conclusion

By following these steps, you can keep your Discord bot running on a Raspberry Pi even when the SSH connection is closed. This is especially useful for maintaining continuous bot functionality.

Feel free to customize the commands according to your specific setup and needs.

---
