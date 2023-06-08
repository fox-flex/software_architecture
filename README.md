# Software architecture

Here are **Software Architecture 2023** course lab tasks.
CS20 APPS UCU

# Description

 - [task](https://docs.google.com/document/d/1uIm9K0KtKpXo6aJWK5pzMY93RSCDG8q108NlIoH_Es4/edit)
 - [report](https://docs.google.com/document/d/1gCD1ktUET1CIVOZZ7aq2EmhT-slfHDWhOvDzGzCDSMk/edit)

# Scripts
- To run
    ```{bash}
    ./start_compose.sh
    ```
- To compleatly clear all docker instances
    ```{bash}
    ./clear.sh
    ```
- To test
    ```{bash}
    ./test.sh
    # or
    ./test_one.sh
    ```
- To track kafka mq
    ```{bash}
    docker run -it --rm --network docker-net -e KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper:2181 bitnami/kafka:latest kafka-console-consumer.sh --bootstrap-server kafka-server:9092 --topic message
    ```

# *Version: branch-name*
* lb1: micro_basics
* lb2: hazelcast
* lb3: micro_hazelcast
* lb4: micro_mq
* lb5: micro_consul
