# Software architecture

Here are **Software Architecture 2023** course lab tasks.
CS20 APPS UCU

# Description
- [task](https://docs.google.com/document/d/1kEndNMGMrvOB10uCP38Sahg56-qAUAEbkyHdDubMrHQ/edit)
- [report](https://docs.google.com/document/d/10fYRwg1tP-jY2uaDYVNTNT2ESGw2iRy_X5b0z96RbZc/edit)

# Installing hazelcast
[guide](https://docs.hazelcast.com/hazelcast/5.3/getting-started/install-hazelcast)
```{bash}
wget -qO - https://repository.hazelcast.com/api/gpg/key/public | gpg --dearmor | sudo tee /usr/share/keyrings/hazelcast-archive-keyring.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/hazelcast-archive-keyring.gpg] https://repository.hazelcast.com/debian stable main" | sudo tee -a /etc/apt/sources.list
sudo apt update && sudo apt install hazelcast=5.3.0 hazelcast-management-center=5.3.0
```

# Run hazelcast
In 3 terminals, run:
```{bash}
hz start -c hazelcast.yaml
```
To start hazelcast management center run: 
```{bash}
hz-mc start -Dhazelcast.mc.http.port=9000 
```
Than you can use provided python scripts for testing.

# *Version: branch-name*
* lb1: micro_basics
* lb2: hazelcast
* lb3: micro_hazelcast
* lb4: micro_mq
* lb5: micro_consul
