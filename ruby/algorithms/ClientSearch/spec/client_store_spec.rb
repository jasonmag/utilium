# spec/client_store_spec.rb
require 'spec_helper'

RSpec.describe ClientFinder::ClientStore do
  let(:json_data) do
    [
      { "id" => 1, "full_name" => "Alice Doe", "email" => "alice@example.com" },
      { "id" => 2, "full_name" => "Bob Smith", "email" => "bob@example.com" }
    ]
  end

  before do
    File.write('spec/temp_clients.json', JSON.generate(json_data))
  end

  after do
    File.delete('spec/temp_clients.json')
  end

  it 'loads clients from a JSON file and wraps them in Client instances' do
    store = ClientFinder::ClientStore.load_from_file('spec/temp_clients.json')
    expect(store.clients.size).to eq(2)
    expect(store.clients.first).to be_a(ClientFinder::Client)
    expect(store.clients.map(&:full_name)).to include("Alice Doe", "Bob Smith")
  end
end
