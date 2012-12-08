#!/usr/bin/ruby
require 'rubygems'
require 'json'

class ViewService
  def self.read()
    json = File.read('../repo/seen.json')
    filter=JSON.parse(json)
    filter 
  end
  
  def self.write(data)
    jsonFile = File.new('../repo/seen.json',"w")
    jsonFile.write(JSON.pretty_generate(data))
    jsonFile.close
  end
  
 
  def self.append(fileName,  user, fullPath)
	filterMap = self.read()
	filterMap[fileName] = {"user"=>user, "time"=>Time.now.utc.to_s, "fullPath"=>fullPath}
	self.write(filterMap)
  end 
  
end
