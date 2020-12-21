# Load_data_to_RDS
This Repository contains coding to load data into database hosted in AWS using python


## To install Python in EC2 Instance
1. Open an EC2 Instance( Make sure to pick a one which falls inside the free tier)
2. Connect to EC2 instance, this can be done by making an SSH connection.
3. For the purpose of doing SSH, I have leveraged WinSCP as the tool.
4. After providing the credentials details like ip address, user name and .ppk file
5. Install putty prior hand, so that you can have terminal access and also to convert .pem file to .ppk file
6. To install python3 in EC2 instance, execute the following command
`sudo yum install python3`
7. I have done the coding in pycharm and executed the SQL commands in Dbeaver.
8. Make sure when EC2 instance is created add an IAM role to access RDS instance. This IAM role will be part of creation of EC2 instance
9. IN RDS instance security group, add security group of EC2 instance with traffic as postgres (5432 port).
    i.e. add security group of EC2 instance in RDS instance.

Load of data seen from dbeaver is shown below ![] 

Loading of data from EC2 instance is shown below ![] 

## Repository contains the following scripts
1. scripts/main.py
2. scripts/utlis.py
3. logs/load_data_to_RDS_instance.log
4. config/config.json
5. scripts/load_details.json  