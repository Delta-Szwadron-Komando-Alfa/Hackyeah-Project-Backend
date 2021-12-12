# API
---
* /upload `POST`<br />
Request body should contain **KEY 'files'** with the value of the files sent to get the types of them

* /validate `POST`<br />
Request body should contain **KEY 'file'** with the value of the file sent to validate if it complies with schema specified inside of it

* /binary `POST`<br />
Request body should contain **KEY 'file'** with the value of the file sent to extract binary files from it
