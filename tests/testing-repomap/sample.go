package main

import "fmt"

type Server struct {
	host string
	port int
}

func NewServer(host string, port int) *Server {
	return &Server{host: host, port: port}
}

func (s *Server) Start() error {
	fmt.Println("starting")
	return nil
}

func (s *Server) Stop() {
	fmt.Println("stopping")
}

func parseConfig(path string) (map[string]string, error) {
	return nil, nil
}
