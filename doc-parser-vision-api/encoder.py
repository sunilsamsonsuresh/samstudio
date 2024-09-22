import json
import base64
import os

# Your JSON data
data = {
  "type": "service_account",
  "project_id": "personal-projects-408314",
  "private_key_id": "8305ce268b5952665845a63fc37b1f9f6cba7bb6",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC2lbNk4rC72LAU\nXA4TnopOGFowYIw/7KNVK9LVTYGa4DFOdHHy5kUMI6f48oAhZ1g2SyaZNgOr1iEl\nM2nJ+e5bhxDlGnjYCLBxijNSzNCsT6JeWHT5h3qqKT0KVRy1dtH2fH/NCCpS9YBe\n71TrcPnF6uaItVuNDOd+2abH0MRVy1Pd3nMUGDBADnpY+w3nb0cYkrxn4VsvBGGi\nL6DGIJuahklLXtzLjFVSJjG4QiqXm7sYEcMpSay7xTit8S8vyzkNiOWaYq7pF/ZA\nxLtgqH2BY5qF6gS/3jhhTggcCtpl2QlaFP7PiXXUqI/bwpJcDF2GJK31HGb8RrOE\ngOoU1Z4bAgMBAAECggEABXPyGL32cB3B7z4Iub5t44gxp9CZu/93WmJoP84JRpml\ntrbF9h/M9eBZ92VXlcBrzQzX5+sYyJZaNhAYccLlwuhntkQ5jQE7Ro0cQ6v7kSMV\nGQzryvUUly+LQpF37tXGHUicDAqUbQMm1eUmoK/EHeUd8OlZ+xvug178Aleer/Ah\nwnvhB+lobSkQcnTp7G6DJCTWRMDCCjPiyuNmzqy8eBu3paHJGVrRObQ+ITsCBOab\napKZZ6GdMnIkyNkIfQxjnyYUS7J9yKkm82U6Gpu5SH2ocfDAZPk2aPASl2nU7fJK\nJ/5H38mSV+n8GnQErRGxh8tWe0mSNldUNjNSPQdR+QKBgQD6UQpdB9iV205LVi+k\ni5oHtIv7/KK3rnBoAaGWPBwKsKGRDVq6n8SUoitD1rBwK1F/HoH4xCn5j9wE+2k5\n9oU0KyvNBqcc2oVK4F+rpMnOXMB1JU1VfDztjcElHyuI2VkchEq0fRxmYbeL6NXC\nFc7q3hJhtJkB3l3Veql8w8iBGQKBgQC6uviAGWa7WEayXG1XOUGdzIOOXPl8TeUS\nxjaephuY5blOzSY7BhO/trcalMUVK81GJfWXhquOhWe+4ko1iKQ6rltMG/FYOdLv\ncFQVWrtzAUKSnj7xEdQhmfZ6sOp7ViQaovRg0dy03ZoHoRy/eJAKqAnUn8PWIn37\nMRNWwQs7UwKBgEzwe+78amYlcntVkm9ROZcEt8JMdPdgdsyBM9mpwDTI9eBP6oNS\neGn3LrU7WCAiMHqSNgDwyrYasdYWMNHQJEFUw7HRSaxkvnO1Y7KuhBkaCU34mTyd\nY1zhJWzzl74IkItjXlL74a7WekRW3N07Ns6aU6wUhrM8Vjs36MCgrRCBAoGATme/\nfBouVq/ET5QbnSo/cQC0pIxJfXY/n1h3Crp4kAS1gG8HhHUSycbwr0qUTkVsFe5O\nZud3FYrSewYNXtkXDES1tQlulzsAZOVniOfmGW4IBARKLXLs/YbmRbIPYuZSlpSh\nxB2abJ8308hEh+kZoj/YkNzcoAcvms+KbTz1eF0CgYBXGIX0gS92prJUwVBqXusq\njTMZ3OqZnqBpyNPSDCUgBE732k5nUMYtCesHw1d0a1xoOVxS1EgcbcfY0l+c6HEm\nc4GjVM4qWLal3m6u9Fuhrb12fqm4uv2ngIkp6xd98kIyJ2gqH68DuJEY6P4iA2Zy\nAN6yDPR7FqKzvSeX0ASBJA==\n-----END PRIVATE KEY-----\n",
  "client_email": "doc-parser@personal-projects-408314.iam.gserviceaccount.com",
  "client_id": "102834277974057387569",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/doc-parser%40personal-projects-408314.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# Convert JSON to string and then encode it to base64
json_str = json.dumps(data)
encoded_json = base64.b64encode(json_str.encode()).decode()

# Print encoded JSON
print(encoded_json)