resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  tags = {
    Name        = "web-server"
    Environment = "production"
  }
}

resource "aws_s3_bucket" "data" {
  bucket = "my-app-data-bucket"
}

resource "aws_security_group" "web_sg" {
  name        = "web-sg"
  description = "Security group for web servers"

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

variable "region" {
  type    = string
  default = "us-east-1"
}

variable "instance_count" {
  type    = number
  default = 2
}

output "web_ip" {
  value = aws_instance.web.public_ip
}
