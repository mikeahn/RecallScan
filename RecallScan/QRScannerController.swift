/*
 barcode scanning code used from tutorial: https://www.appcoda.com/barcode-reader-swift/
 */

import UIKit
import AVFoundation

extension NSMutableAttributedString {
    public func setAsLink(textToFind:String, linkURL:String) -> Bool {
        
        let foundRange = self.mutableString.range(of: textToFind)
        if foundRange.location != NSNotFound {
            
            self.addAttribute(.link, value: linkURL, range: foundRange)
            
            return true
        }
        return false
    }
}

class QRScannerController: UIViewController, AVCaptureMetadataOutputObjectsDelegate {
    
    var captureSession:AVCaptureSession?
    var videoPreviewLayer:AVCaptureVideoPreviewLayer?
    var qrCodeFrameView:UIView?

    @IBOutlet var messageLabel:UILabel!
    @IBOutlet var topbar: UIView!
    @IBOutlet weak var popupView: UIView!
    @IBOutlet weak var title1: UILabel!
    @IBOutlet weak var title2: UILabel!
    @IBOutlet weak var title3: UILabel!
    @IBOutlet weak var title4: UILabel!
    @IBOutlet weak var title5: UILabel!
    @IBOutlet weak var item1: UILabel!
    @IBOutlet weak var item2: UILabel!
    @IBOutlet weak var item3: UILabel!
    @IBOutlet weak var item4: UILabel!
    @IBOutlet weak var item5: UILabel!
    @IBOutlet weak var urlOutlet: UITextView!
    @IBOutlet weak var buttonView: UIImageView!
    
    var json:[[String : Any]] = []
    var update = false
    var titles:[UILabel] = []
    var items:[UILabel] = []
    var metaDataPrev: String = ""
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        let deviceDiscoverySession = AVCaptureDevice.DiscoverySession(deviceTypes: [.builtInDualCamera], mediaType: AVMediaType.video, position: .back)
        
        guard let captureDevice = deviceDiscoverySession.devices.first else {
            print("Failed to get the camera device")
            return
        }
        do {
            let input = try AVCaptureDeviceInput(device: captureDevice)
            
            captureSession = AVCaptureSession()
            captureSession?.addInput(input)
            
            let captureMetadataOutput = AVCaptureMetadataOutput()
            captureSession?.addOutput(captureMetadataOutput)
            
            captureMetadataOutput.setMetadataObjectsDelegate(self, queue: DispatchQueue.main)
            captureMetadataOutput.metadataObjectTypes = [AVMetadataObject.ObjectType.qr, AVMetadataObject.ObjectType.upce,
                AVMetadataObject.ObjectType.code39,
                AVMetadataObject.ObjectType.code39Mod43,
                AVMetadataObject.ObjectType.code93,
                AVMetadataObject.ObjectType.code128,
                AVMetadataObject.ObjectType.ean8,
                AVMetadataObject.ObjectType.ean13,
                AVMetadataObject.ObjectType.aztec,
                AVMetadataObject.ObjectType.pdf417,
                AVMetadataObject.ObjectType.itf14,
                AVMetadataObject.ObjectType.interleaved2of5,
                AVMetadataObject.ObjectType.dataMatrix]
            
            videoPreviewLayer = AVCaptureVideoPreviewLayer(session: captureSession!)
            videoPreviewLayer?.videoGravity = AVLayerVideoGravity.resizeAspectFill
            videoPreviewLayer?.frame = view.layer.bounds
            view.layer.addSublayer(videoPreviewLayer!)
            
            view.bringSubview(toFront: messageLabel)
            view.bringSubview(toFront: topbar)
            
            qrCodeFrameView = UIView()
            if let qrCodeFrameView = qrCodeFrameView {
                qrCodeFrameView.layer.borderColor = UIColor.green.cgColor
                qrCodeFrameView.layer.borderWidth = 2
                view.addSubview(qrCodeFrameView)
                view.bringSubview(toFront: qrCodeFrameView)
            }
            
        } catch {
            print(error)
            return
        }
        captureSession?.startRunning()
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    func metadataOutput(_ output: AVCaptureMetadataOutput, didOutput metadataObjects: [AVMetadataObject], from connection: AVCaptureConnection) {
        
        if metadataObjects.count == 0 {
            qrCodeFrameView?.frame = CGRect.zero
            messageLabel.text = "No Barcode is detected"
            for n in 0...4 {
                titles[n].text = ""
                items[n].text = ""
            }
            let attributedString = NSMutableAttributedString(string: "")
            urlOutlet.attributedText = attributedString
            popupView.isHidden = true
            buttonView.isHidden = true
            
            return
        }
        
        let metadataObj = metadataObjects[0] as! AVMetadataMachineReadableCodeObject
        
        if [AVMetadataObject.ObjectType.qr,
        AVMetadataObject.ObjectType.upce,
        AVMetadataObject.ObjectType.code39,
        AVMetadataObject.ObjectType.code39Mod43,
        AVMetadataObject.ObjectType.code93,
        AVMetadataObject.ObjectType.code128,
        AVMetadataObject.ObjectType.ean8,
        AVMetadataObject.ObjectType.ean13,
        AVMetadataObject.ObjectType.aztec,
        AVMetadataObject.ObjectType.pdf417,
        AVMetadataObject.ObjectType.itf14,
        AVMetadataObject.ObjectType.interleaved2of5, AVMetadataObject.ObjectType.dataMatrix].contains(metadataObj.type) {
            
            let barCodeObject = videoPreviewLayer?.transformedMetadataObject(for: metadataObj)
            qrCodeFrameView?.frame = barCodeObject!.bounds
            
            if metadataObj.stringValue != nil {
                if metaDataPrev == "" || metaDataPrev != metadataObj.stringValue {
                    self.update = true
                } else {
                    self.update = false
                }
                metaDataPrev = metadataObj.stringValue!
                if (metaDataPrev.count > 12) {
                    metaDataPrev = String(metaDataPrev.suffix(12))
                }
                print(metaDataPrev)
                
                let displayString = "Item Found"
                let urlString = "http://recallscan.online:5000/api/v1/upc/?code=" + metaDataPrev
                let url = URL(string:urlString)
                
                let task = URLSession.shared.dataTask(with: url!) {(data, response, error) in
                    guard let data = data else { return }
                    do {
                        let newJson = try JSONSerialization.jsonObject(with: data, options: []) as! [[String: Any]]
                        if (self.json.count == 0) {
                            self.json = newJson
                            //self.update = true
                        }
                        else if (newJson.count == 0 || self.json[0]["code"] as! String != newJson[0]["code"] as! String) {
                            self.json = newJson
                           // self.update = true
                        }
                    }
                    catch {
                        print(error)
                        return
                    }
                }
                
                titles = [self.title1, self.title2, self.title3, self.title4, self.title5]
                items = [self.item1, self.item2, self.item3, self.item4, self.item5]
                
                if (json.count != 0) {
                    print("hit")
                    titles[0].text = "Brand: "
                    items[0].text = json[0]["brandName"] as? String
                    titles[1].text = "Company: "
                    items[1].text = json[0]["companyName"] as? String
                    titles[2].text = "Reason: "
                    items[2].text = json[0]["recallReason"] as? String
                    titles[3].text = "Code: "
                    items[3].text = json[0]["code"] as? String
                    titles[4].text = "Desc: "
                    items[4].text = json[0]["productDescription"] as? String
                    let firstUrl = json[0]["url"] as? String
                    let fullUrl = firstUrl!.trimmingCharacters(in:.whitespacesAndNewlines)
                    urlOutlet.isEditable = false
                    urlOutlet.dataDetectorTypes = UIDataDetectorTypes.all
                    
                    let attributedString = NSMutableAttributedString(string: "Click To Read More")
                    attributedString.addAttribute(.link, value: fullUrl, range: NSRange(location: 0, length:18))
                    urlOutlet.attributedText = attributedString
                    urlOutlet.textAlignment = NSTextAlignment.center
                    urlOutlet.textColor = UIColor.blue
                    urlOutlet.font = UIFont.systemFont(ofSize: 30)
                    buttonView.image = UIImage(named: "recallButton")
                    
                    for n in 0...4 {
                        titles[n].numberOfLines = 1
                        titles[n].font = UIFont.systemFont(ofSize: 15)
                        items[n].numberOfLines = 1
                        items[n].adjustsFontSizeToFitWidth = true
                    }
                    update = false
                }
                else {
                    print("safe")
                    for n in 0...4 {
                        titles[n].text = ""
                        items[n].text = ""
                    }
                    let attributedString = NSMutableAttributedString(string: "Safe!")
                    urlOutlet.attributedText = attributedString
                    urlOutlet.textAlignment = NSTextAlignment.center
                    urlOutlet.textColor = UIColor.black
                    urlOutlet.font = UIFont.systemFont(ofSize: 35)
                    buttonView.image = UIImage(named: "safeButton")
                }
                
                popupView.layer.cornerRadius = 10.0
                
                self.view.addSubview(self.popupView)
                self.view.bringSubview(toFront: self.popupView)
                
                self.view.addSubview(self.buttonView)
                self.view.bringSubview(toFront: self.buttonView)
                
                self.popupView.isHidden = false
                self.buttonView.isHidden = false
                messageLabel.text = displayString
                task.resume()
                
            }
        }
    }
}
