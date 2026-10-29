import Foundation
import CoreImage

guard CommandLine.arguments.count == 2,
      let image = CIImage(contentsOf: URL(fileURLWithPath: CommandLine.arguments[1])),
      let detector = CIDetector(ofType: CIDetectorTypeQRCode, context: nil,
                                options: [CIDetectorAccuracy: CIDetectorAccuracyHigh]) else {
    fatalError("Could not open QR image")
}
let messages = detector.features(in: image).compactMap { ($0 as? CIQRCodeFeature)?.messageString }
guard messages.count == 1 else { fatalError("Expected one QR code; found \(messages.count)") }
print(messages[0])
