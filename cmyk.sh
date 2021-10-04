#!/bin/bash
# https://makandracards.com/makandra/1489-convert-the-colorspace-of-a-pdf-from-rgb-to-cmyk-under-ubuntu-linux
f="$1" ; shift
c="${f%.pdf}_cmyk.pdf"
gs -dSAFER -dBATCH -dNOPAUSE -dNOCACHE \
    -sDEVICE=pdfwrite \
    -sColorConversionStrategy=CMYK -sColorConversionStrategyForImages=CMYK \
    -sProcessColorModel=DeviceCMYK \
    -sOutputFile="$c" "$f"
