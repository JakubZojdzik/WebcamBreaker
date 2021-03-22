modprobe -r v4l2loopback
modprobe v4l2loopback devices=1 video_nr=2 card_label="Fake" exclusive_caps=1