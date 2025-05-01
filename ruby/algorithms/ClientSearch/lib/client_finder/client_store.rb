require_relative 'client'

module ClientFinder
  class ClientStore
    attr_reader :clients

    def initialize(clients)
      @clients = clients
    end

    def self.load_from_file(path)
      data = JSON.parse(File.read(path))
      new(data.map { |c| Client.new(c) })
    end
  end
end
