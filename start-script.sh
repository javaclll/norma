/usr/sbin/sshd -D &

autossh -M 0 -i /keys/id_rsa -o PubkeyAuthentication=yes -o PasswordAuthentication=no -o StrictHostKeyChecking=no -N -R 0:localhost:22 ubuntu@155.248.247.182 &

export GIT_SSH_COMMAND="ssh -o StrictHostKeyChecking=no"

cd /home/ubuntu && git clone git@github.com:arpandaze/norma.git && cd /home/ubuntu/norma/norma && git checkout hpc && python -m norma train $MODEL_NAME &

tail -f /dev/null
