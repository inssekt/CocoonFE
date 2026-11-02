require "json"
require "yaml"

def check(node, where)
  case node
  when Psych::Nodes::Mapping
    keys = node.children.each_slice(2).map { |key, _| key.respond_to?(:value) ? key.value : key.to_s }
    repeated = keys.find { |key| keys.count(key) > 1 }
    raise "#{where}: #{repeated} is set twice" if repeated
    node.children.each_slice(2) { |key, value| check(value, "#{where} > #{key.respond_to?(:value) ? key.value : key}") }
  when Psych::Nodes::Sequence
    node.children.each_with_index { |value, i| check(value, "#{where} > #{i + 1}") }
  when Psych::Nodes::Alias
    raise "#{where}: anchors and aliases aren't supported"
  end
end

out = {}
ARGV.each do |path|
  name = File.basename(path, ".yaml")
  begin
    text = File.read(path, encoding: "UTF-8")
    tree = Psych.parse(text)
    check(tree.root, name) if tree
    out[name] = YAML.safe_load(text, permitted_classes: [], aliases: false)
  rescue StandardError => e
    warn "#{name}: #{e.message}"
    exit 1
  end
end
puts JSON.generate(out)
