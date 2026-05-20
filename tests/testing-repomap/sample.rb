require 'json'
require 'net/http'

module Formatter
  def format_output(data)
    JSON.generate(data)
  end

  def parse_input(raw)
    JSON.parse(raw)
  end
end

class DataProcessor
  include Formatter

  def initialize(config)
    @config = config
    @cache = {}
  end

  def process(data)
    key = data.hash.to_s
    @cache[key] ||= transform(data)
  end

  def validate(input)
    !input.nil? && !input.empty?
  end

  private

  def transform(data)
    data
  end
end

class ApiClient < DataProcessor
  def fetch(url)
    URI.parse(url)
  end
end

def parse_args(args)
  args.each_with_object({}) do |arg, memo|
    k, v = arg.split('=')
    memo[k] = v
  end
end
