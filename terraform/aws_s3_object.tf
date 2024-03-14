resource "null_resource" "update_asset_path" {
  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    command = <<EOF
sed -i '' 's|"/assets/|"/marathons/assets/|g' ${path.module}/../dist/index.html
sed -i '' 's|"/favicon.ico|"/marathons/favicon.ico|g' ${path.module}/../dist/index.html
EOF
  }
}


resource "aws_s3_object" "static_file" {
  depends_on = [ null_resource.update_asset_path ]

  for_each     = fileset(local.website_dir, "**")
  bucket       = aws_s3_bucket.static_website.id
  key          = each.key
  source       = "${local.website_dir}/${each.value}"
  content_type = lookup(local.content_types, regex("\\.[^.]+$", each.value), null)
  etag         = filemd5("${local.website_dir}/${each.value}")
}