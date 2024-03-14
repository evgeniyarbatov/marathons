resource "aws_s3_object" "static_file" {
  for_each     = fileset(local.website_dir, "**")
  bucket       = aws_s3_bucket.static_website.id
  key          = "marathons/${each.key}"
  source       = "${local.website_dir}/${each.value}"
  content_type = lookup(local.content_types, regex("\\.[^.]+$", each.value), null)
  etag         = filemd5("${local.website_dir}/${each.value}")
}