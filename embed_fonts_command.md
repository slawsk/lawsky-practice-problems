gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite \
   -dEmbedAllFonts=true \
   -dSubsetFonts=true \
   -dPDFSETTINGS=/prepress \
   -sOutputFile=output.pdf input.pdf
