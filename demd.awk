$0=="```"       { flag+=1; next; }
$0=="```rapira" { flag+=1; next; }
flag==1         { print; }
