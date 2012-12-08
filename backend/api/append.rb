#!/usr/bin/ruby
require '../service/ViewService.rb'
require 'cgi'


puts "Content-Type: text/plain"
puts

cgi=CGI.new

#fullPath="fullPath"
#user="user"
#fileName="fileName"

fullPath=cgi['fullPath']
user=cgi['user'] 
fileName=cgi['fileName']



if !fullPath.empty? && !user.empty? && !fileName.empty?
  ViewService.append(fileName, user, fullPath)
  puts "data store"
else
 puts "Error user and path should be set"
end


