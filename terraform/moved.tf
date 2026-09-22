moved {
  from = module.fastapi.docker_image.fastapi
  to   = module.fastapi.docker_image.kimai
}

moved {
  from = module.fastapi.docker_container.fastapi
  to   = module.fastapi.docker_container.kimai
}
