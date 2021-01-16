# base image
FROM ubuntu:18.04

# define user and group
ARG USER_ID
ARG GROUP_ID

# install Starspace and essential libs
RUN apt -y update && \
    apt -y install git wget zip make g++ && \
	wget https://dl.bintray.com/boostorg/release/1.63.0/source/boost_1_63_0.zip && \
	unzip boost_1_63_0.zip && \
	mv boost_1_63_0 /usr/local/bin && \
	git clone https://github.com/facebookresearch/Starspace.git && \
	cd Starspace && \
	make

# create a new user with group
RUN addgroup --gid $GROUP_ID new_user
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID new_user

# switch to a new user
USER new_user

# select working directory
WORKDIR /Starspace

# command to execute (generate embeddings for the input file)
CMD ./starspace train -trainFile /home/new_user/volume/input.txt -model /home/new_user/volume/starspace_output -trainMode 5

