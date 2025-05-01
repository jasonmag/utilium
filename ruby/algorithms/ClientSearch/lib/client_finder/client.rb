module ClientFinder
  class Client
    attr_reader :id, :full_name, :email

    def initialize(attrs)
      @id = attrs["id"]
      @full_name = attrs["full_name"]
      @email = attrs["email"]
    end

    def to_h
      { id: id, full_name: full_name, email: email }
    end
  end
end
