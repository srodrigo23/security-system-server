from firebase_manager import send_push

# we need token frm android app
tokens = ["f5vjCZtXR56JiHGTnzUgLU:APA91bGz2UTbdU_MxPYfuN4Xqip7uGchcD3EKS7jVhicnvnRpOi4m4v4LZEjutdM8Bbbad8XQVqrpVSGz2hNq_8_HjK11BnGMaTf5W6IxNlVXZBHE-8rSmChMdnVpGcz39ezwlGUs03A"]

send_push("Hola", "este es un mensaje desde el servidor", tokens)
