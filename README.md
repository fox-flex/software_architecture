# Software architecture

Here are **Software Architecture 2023** course lab tasks.
CS20 APPS UCU

# Description

 - [task](https://docs.google.com/document/d/1_DCyflPIPCw0-uPTA1xNc3-8m2aUn1mloxOnP1UJ6ho/edit)
 - [report](https://docs.google.com/document/d/1U_niSISsY4pxj3SZhXh9tCea0tI5vheTHNicdRDZbFU/edit)

# To run
```{bash}
./start_compose.sh
```

# To run requests
- Post
    ```{bash}
    curl -d '{"text":"fox flex 1"}' -H "Content-Type: application/json" -X POST http://localhost:8000/
    ```

- Get
    ```{bash}
    curl http://localhost:8000/
    ```

# *Version: branch-name*
* lb1: micro_basics
* lb2: hazelcast
* lb3: micro_hazelcast
* lb4: micro_mq
* lb5: micro_consul
