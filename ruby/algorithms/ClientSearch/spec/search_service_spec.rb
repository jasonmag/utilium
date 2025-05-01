# spec/search_service_spec.rb
require 'spec_helper'

RSpec.describe ClientFinder::SearchService do
  let(:clients) do
    [
      ClientFinder::Client.new({ "id" => 1, "full_name" => "Jane Smith", "email" => "jane@example.com" }),
      ClientFinder::Client.new({ "id" => 2, "full_name" => "John Doe", "email" => "john@example.com" }),
      ClientFinder::Client.new({ "id" => 3, "full_name" => "Another Jane", "email" => "jane@example.com" })
    ]
  end

  let(:store) { ClientFinder::ClientStore.new(clients) }
  let(:service) { ClientFinder::SearchService.new(store) }

  describe '#by_field' do
    it 'finds clients by full_name with partial match' do
      result = service.by_field("full_name", "Jane")
      expect(result.map(&:full_name)).to contain_exactly("Jane Smith", "Another Jane")
    end

    it 'finds clients by email with partial match' do
      result = service.by_field("email", "john")
      expect(result.map(&:email)).to include("john@example.com")
    end

    it 'returns empty when field does not exist' do
      result = service.by_field("nonexistent", "anything")
      expect(result).to eq([])
    end

    it 'returns empty when there is no match' do
      result = service.by_field("full_name", "XYZ")
      expect(result).to eq([])
    end
  end

  describe '#duplicate_emails' do
    it 'returns clients with duplicate emails' do
      result = service.duplicate_emails
      expect(result.size).to eq(2)
      expect(result.map(&:email).uniq).to eq(["jane@example.com"])
    end

    it 'returns empty when no duplicates are found' do
      store = ClientFinder::ClientStore.new([
        ClientFinder::Client.new({ "id" => 1, "full_name" => "Jane Smith", "email" => "jane@example.com" }),
        ClientFinder::Client.new({ "id" => 2, "full_name" => "John Doe", "email" => "john@example.com" })
      ])
      service = ClientFinder::SearchService.new(store)
      expect(service.duplicate_emails).to be_empty
    end
  end
end
