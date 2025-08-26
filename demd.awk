$0=="```" { flag+=1; next; }
flag==1   { print; }
