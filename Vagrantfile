# Vagrantfile to build a box with the required software for this library.

$script = <<SCRIPT
sudo apt-get update
sudo apt-get install python3-setuptools
sudo easy_install3 pip
sudo pip3 install nose
SCRIPT


Vagrant.configure(2) do |config|
  config.vm.box = "bento/ubuntu-16.04"
  config.vm.provision "shell", inline: $script
end
