Update stories
set text = REPLACE( REPLACE( REPLACE( text, CHAR(13), ' '), CHAR(11), ' '), CHAR(10), ' ')