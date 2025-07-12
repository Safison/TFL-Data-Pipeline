variable "extract_lambda" {
  type    = string
  default = "extract"
}

variable "transform_lambda" {
  type    = string
  default = "transfrom"
}

variable "default_timeout" {
  type    = number
  default = 5
}