resource "digitalocean_ssh_key" "terraform" {
  name       = "terraform"
  public_key = "${file(var.ssh_public_key)}"
}

resource "digitalocean_droplet" "transientvpn" {
  image    = "freebsd-11-1-x64"
  name     = "${var.droplet_name}"
  region   = "${var.region}"
  size     = "${var.droplet_size}"
  ipv6     = true
  ssh_keys = [
    "${var.ssh_fingerprint}"
  ]

  provisioner "file" {
    source        = "./install_python27.sh"
    destination   = "/usr/home/freebsd/install_python27.sh"

    connection {
      user        = "freebsd"
      type        = "ssh"
      private_key = "${file(var.ssh_private_key)}"
      timeout     = "2m"
    }
  }

  provisioner "remote-exec" {
    inline = [
      "sudo chmod u+x /usr/home/freebsd/install_python27.sh",
      "sudo /usr/home/freebsd/install_python27.sh"
    ]
    connection {
      user        = "freebsd"
      type        = "ssh"
      private_key = "${file(var.ssh_private_key)}"
      timeout     = "2m"
    }
  }
}
