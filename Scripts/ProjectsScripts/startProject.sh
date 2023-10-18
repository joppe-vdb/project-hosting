#!/bin/bash
# move to the correct directory
cd /home/ccs5/projects/$1/config

# get the vm to join the cluster
export KUBECONFIG=/home/ccs5/cluster/ccs5-cluster.yaml

# execute the following commando's with kubectl to setup the pod (option validate=false to ignore authentication)
kubectl apply -f $1-namespace.yaml --validate=false # namespace
kubectl apply -f $1-pv.yaml --validate=false # presistentvolume
kubectl apply -f $1-pvc.yaml --validate=false # persistentvolumeclaim 
kubectl apply -f $1-mysql-deployment.yaml --validate=false # deployment
kubectl apply -f $1-mysql-service.yaml --validate=false # service mysql
kubectl apply -f $1-laravel-deployment.yaml --validate=false # deployment
kubectl apply -f $1-laravel-service.yaml --validate=false # service laravel
kubectl apply -f $1-loadbalancer.yaml --validate=false # loadbalancer
