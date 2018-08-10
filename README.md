# metavault
Modify XML data from a ResourceSpace filestore

## Requirements
- Vagrant
- Python 3
- py3exiv2
- xmltodict

## Automatic setup
```bash
source vagrant_setup.sh
```

## Troubleshooting

### py3exiv2 won't install
- Check that Vagrant has at least 2 GB of RAM if receiving this error: ```error: command 'x86_64-linux-gnu-gcc' failed with exit status 4```
