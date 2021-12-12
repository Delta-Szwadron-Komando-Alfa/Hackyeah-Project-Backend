# API
---
* /upload `POST`
Request body should contain **KEY 'files'** with the value of the files sent to get the types of them

* /validate `POST`
Request body should contain **KEY 'file'** with the value of the file sent to validate if it complies with schema specified inside of it

* /binary `POST`
Request body should contain **KEY 'file'** with the value of the file sent to extract binary files from it
