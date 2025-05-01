module ClientFinder
  class SearchService
    def initialize(store)
      @store = store
    end

    def by_field(field, query)
      @store.clients.select do |c|
        value = c.send(field) rescue nil
        value&.to_s&.downcase&.include?(query.downcase)
      end
    end

    def duplicate_emails
      grouped = @store.clients.group_by { |c| c.email.downcase }
      grouped.select { |_, v| v.size > 1 }.values.flatten
    end
  end
end
