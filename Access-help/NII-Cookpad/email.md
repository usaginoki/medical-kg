# Email: NII IDR Cookpad Dataset, pre-application inquiry

- **To:** NII IDR office <idr@nii.ac.jp>
- **Cc:** Dr. Fajri Koto (supervisor)
- **Why an email first:** the formal procedure (https://www.nii.ac.jp/dsc/idr/cookpad/, section 必要書類) is:
  1. fill in the application form 利用申請書 (`application_ckpd_1_4.docx`) and email it with the subject
     「クックパッドデータ利用申請（<University>）」;
  2. someone with contract authority (usually dean level) signs the agreement 同意書, stamps it with the official seal and
     posts it to NII;
  3. notify NII 30 days before publishing, and send a yearly usage report.

  It is aimed at university and public research institutes, and the docs are Japanese-centric. Before doing the
  paperwork it's worth confirming that (a) an overseas university (MBZUAI, UAE) is eligible, and (b) how the terms treat
  LLM use. Feeding the data to an external generative-AI service counts as third-party disclosure unless the provider
  guarantees no training on inputs.
- **Alternative for non-academic use:** Cookpad directly, recipe-corpus@cookpad.com
- **Files, if approved:** 7z MySQL dump (~1.8 GB, ~5.5 GB unpacked). Extract the recipe tables to `Data/nii-cookpad-dataset/`.

---

**Subject:** クックパッドデータ利用申請に関する事前問い合わせ（Mohamed bin Zayed University of Artificial Intelligence） / Inquiry about applying for the Cookpad dataset (MBZUAI, UAE)

国立情報学研究所 情報学研究データリポジトリ ご担当者様

Mohamed bin Zayed University of Artificial Intelligence（MBZUAI、アラブ首長国連邦）の Artur Pak と申します。
Fajri Koto 先生の指導のもと、食文化を考慮した健康アドバイス AI の学術研究を行っております。
クックパッドデータセットの利用申請を検討しており、申請前に以下の点をご確認させていただきたく、ご連絡いたしました。
（以下、英語で失礼いたします。）

Dear IDR team,

I am a student at MBZUAI in Abu Dhabi, working under the supervision of Dr. Fajri Koto. Our team does academic research
on AI assistants for health questions that take users' food cultures into account. Japanese home cooking is one of the
cuisines we study, and the Cookpad dataset (Harashima et al., LREC 2016) would be very valuable to us. Before preparing
the application form and the agreement, may I ask:

1. Are researchers at a university outside Japan (MBZUAI, United Arab Emirates) eligible to apply? If so, is an English
   version of the application form and agreement available, and can the agreement be signed by our university's
   authorised signatory without a Japanese-style official seal (公印)?
2. Our research uses large language models. We understand that sending the data to external generative-AI services is
   restricted. Would running open-weight models on our own servers be acceptable? Would a commercial API whose terms
   guarantee that inputs are not used for training also be acceptable?

The data would be used only for non-commercial academic research within our group. We would follow all the terms,
including advance notice of publications and annual reports.

Thank you very much for your help.

Best regards,
Artur Pak
Department of Natural Language Processing, Mohamed bin Zayed University of Artificial Intelligence (MBZUAI), Abu Dhabi, UAE
Supervisor: Dr. Fajri Koto
artur.pak@mbzuai.ac.ae
