#!/usr/bin/ruby
require '../service/ViewService.rb'
require 'cgi'


puts "Content-Type: text/plain"
puts

cgi=CGI.new




data = ViewService.read()

puts JSON.pretty_generate(data)


