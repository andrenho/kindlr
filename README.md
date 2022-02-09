# kindlr
Converts epub/pdf files to kindle format, and mails them to kindle.

# Requirements

**kindlegen** is required. Download it from
[here](https://archive.org/download/kindlegen_linux_2_6_i386_v2_9/kindlegen_linux_2.6_i386_v2_9.tar.gz)
and place in somewhere in the path.

**s-nail** is also required. Get it from your package manager. Configure it in ~/.mailrc.

# Usage

Create a config file `$HOME/.kindlr` with the following content:

```sh
email_to=dest@free.kindle.com
```

Convert and push file to kindle with the following command:

```sh
kindlr [-k] mybook.epub
```

The `-k` option will skip the convertion and send the file directly. Useful for pdfs.
