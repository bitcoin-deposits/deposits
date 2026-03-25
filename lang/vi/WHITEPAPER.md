# bitcoin deposits
## tóm tắt

một phiên bản ngang hàng lý tưởng của tiền mặt điện tử sẽ cho phép các khoản thanh toán trực tuyến được gửi trực tiếp từ bên này sang bên kia một cách nhanh chóng và với sự chuẩn bị tối thiểu. mạng lightning cung cấp một phần giải pháp, nhưng những lợi ích thiết yếu sẽ bị mất nếu một bên thứ ba đáng tin cậy được yêu cầu quản lý trạng thái thay mặt bạn. chúng tôi đề xuất một giải pháp cho vấn đề này bằng cách sử dụng các sổ cái có thể xác minh và một mạng lưới thế chấp. các nhà vận hành phát các bản cập nhật sổ cái tới các đồng nghiệp của họ, tạo ra một bản ghi tài khoản có thể kiểm toán. các ví phát bằng chứng về sự không trung thực tới những đồng nghiệp đó, những người đảm bảo rằng sổ cái duy trì một nhà vận hành trung thực. việc rút tiền đơn phương được thay thế bởi sự đảm bảo rằng tiền vẫn khả dụng miễn là mạng còn hoạt động. chúng tôi đạt đến một mạng lưới ủy thác việc duy trì thanh khoản, tránh phí thiết lập, có khả năng nhận thanh toán ngoại tuyến, và mở rộng độc lập với lớp cơ sở

## giới thiệu

bitcoin deposits nhằm cung cấp các khoản tiền được kiểm soát bằng khóa, nhanh chóng và có khả năng mở rộng, không cần tin cậy, ngoài chuỗi. hoạt động trên chuỗi mở rộng theo số lượng sổ cái và tần suất luân chuyển dự trữ. thông lượng mở rộng hơn một chút so với tuyến tính theo số lượng sổ cái trong mạng, khiến hàng triệu giao dịch mỗi giây trên hàng nghìn tỷ ví trở nên khả thi

có những sự đánh đổi rõ ràng:
- không có lối thoát đơn phương: khi các nhà vận hành thất bại, tiền vẫn ở lại trong mạng
- không có quyền riêng tư: việc xác minh đòi hỏi sự minh bạch
- khả dụng không liên tục: một khoản tiền gửi chỉ khả dụng như nhà vận hành của nó. các ví nên phân bổ tiền để tăng khả dụng

chúng tôi kỳ vọng trải nghiệm ví sẽ tương tự như một lớp cơ sở nhanh, có kinh tế thanh toán tương tự như mạng lightning

## sổ cái

một sổ cái là một chuỗi bất biến các bản cập nhật, chứa hash của bản cập nhật trước đó và được ký bởi nhà vận hành của sổ cái. các loại bản cập nhật khác nhau có các quy tắc khác nhau về thời điểm và cách chúng có thể được sử dụng. các sổ cái tự mô tả, các bản cập nhật của chúng có sẵn công khai và không thể phủ nhận, cho phép bất kỳ ai đánh giá sự tuân thủ

các sổ cái có một nhà vận hành đang hoạt động duy nhất, nhưng được duy trì hợp tác bởi mạng lưới. bất kỳ nhà vận hành nào cũng có thể tạo một sổ cái, nhưng nếu họ biến mất hoặc trở nên không trung thực, một nhà vận hành khác sẽ được chỉ định, cùng với dự trữ. nhà vận hành đang hoạt động hiện tại được xác định bởi khóa công khai được sử dụng để ký bản cập nhật đồng ký gần nhất

## tiền gửi

một tiền gửi là một tài khoản ổn định có thể gửi và nhận tiền, được kiểm soát bởi miniscript. khi mở, một lịch phí được thiết lập, cũng như việc nhận tiền có yêu cầu yêu cầu được ví ký hay không. một nhà vận hành phải cho phép chuyển tiền giữa các tiền gửi trên cùng một sổ cái cũng như rút tiền trên chuỗi. họ nên cho phép các tiền gửi thanh toán hóa đơn lightning

việc tạo các đề nghị cấp vốn trên chuỗi hoặc hóa đơn lightning thay mặt cho một tiền gửi nằm trong quyền quyết định của nhà vận hành. nếu họ làm vậy, những thứ này nên được đồng ký bởi một thành viên hội đồng, và ví nên xác minh chữ ký này. các đề nghị và hóa đơn không phải là một phần của sổ cái, vì vậy ví có trách nhiệm xác minh chữ ký và lưu giữ chúng làm bằng chứng

## phí

chuyển tiền giữa các tiền gửi, trên chuỗi, và qua lightning có phí trả cho nhà vận hành của sổ cái. cũng có phí được áp dụng định kỳ cho số dư với một chu kỳ cụ thể. tất cả đều được thương lượng khi mở một tiền gửi mới. phí có thể được thay đổi sau một số khối nhất định, với thông báo trước một số khối nhất định và trong giới hạn phần trăm mỗi lần điều chỉnh được thương lượng khi mở. hội đồng có thể từ chối đồng ký các bản cập nhật tạo ra các tình huống không có lợi nhuận mà họ có thể phải chịu trách nhiệm cuối cùng

## chuyển tiền

hình thức cơ bản của chuyển tiền là một thao tác hai giai đoạn giữa hai tiền gửi trên cùng một sổ cái: một tiền gửi phát hành một yêu cầu gửi tiền. nếu có đủ tiền khả dụng, một khóa trên số tiền với điều kiện chi tiêu được thêm vào sổ cái. nếu điều kiện chi tiêu được thỏa mãn trước thời hạn, tiền chuyển từ người gửi sang người nhận trừ phí của nhà vận hành. nếu hết thời hạn, khóa được giải phóng, trừ một khoản phí nhà vận hành nhỏ hơn. với các điều kiện chi tiêu miniscript, điều này đủ để cho phép bất kỳ tiền gửi nào cung cấp cầu nối và dịch vụ thanh khoản cho các tiền gửi khác trên cùng sổ cái

## lightning

các nhà vận hành có kênh lightning có thể cho phép các tiền gửi gửi và nhận qua mạng lightning. khi một tiền gửi yêu cầu một hóa đơn lightning, nhà vận hành tạo một hóa đơn thông qua nút lightning của họ, yêu cầu các thành viên hội đồng đồng ký để chứng minh họ cam kết ghi có cho tiền gửi khi thanh toán. ví nên lưu giữ hóa đơn đồng ký này làm bằng chứng. khi một tiền gửi yêu cầu thanh toán một hóa đơn lightning, nhà vận hành thanh toán bằng nút lightning của họ và ghi nợ tiền gửi sau khi có được preimage

khi người trả và người nhận đều là tiền gửi trên cùng một nhà vận hành, nhà vận hành có thể thanh toán nội bộ mà không cần định tuyến qua lightning, ghi có và ghi nợ trực tiếp các tiền gửi tương ứng. điều này tránh được phí định tuyến và các chế độ lỗi trong khi vẫn duy trì các đảm bảo kế toán tương tự

## người chuyển phát

các yêu cầu chuyển tiền chỉ di chuyển tiền giữa các tiền gửi trên cùng một sổ cái. để di chuyển tiền qua các sổ cái, ví sử dụng người chuyển phát — các dịch vụ nắm giữ tiền gửi trên nhiều sổ cái và mang chuyển tiền giữa chúng. một người chuyển phát quảng cáo dung lượng và phí theo hướng trên mỗi sổ cái trên relay. khi một ví muốn gửi từ sổ cái A sang sổ cái B, nó tạo một khóa chuyển tiền tới tiền gửi của người chuyển phát và yêu cầu người chuyển phát tạo một khóa từ tiền gửi của họ trên sổ cái đích đến cho người nhận. khi cả hai khóa được thiết lập, ví tiết lộ preimage cho người nhận, người này hoàn tất chuyển tiền từ người chuyển phát. sau khi tiết lộ, người chuyển phát sử dụng cùng preimage này để hoàn tất chuyển tiền từ người gửi tới người chuyển phát

đây là một mẫu hợp đồng khóa theo thời gian và hash tiêu chuẩn. chúng tôi kỳ vọng thời hạn hết hạn của người chuyển phát sẽ sớm hơn nghiêm ngặt so với thời hạn đến, đảm bảo rằng nếu ví không bao giờ tiết lộ, cả hai khóa đều hết hạn và không bên nào mất tiền. không cần tin cậy ngoài đảm bảo thời hạn được các nhà vận hành thực thi

người chuyển phát nên đặt phí theo sổ cái: fee_in và fee_out cho mỗi sổ cái họ phục vụ. ví ước tính chi phí tuyến đường là fee_out trên nguồn cộng với fee_in trên đích. người chuyển phát có thể thay đổi phí theo sổ cái dựa trên thanh khoản khả dụng, tự nhiên tái cân bằng vị thế của họ. ví khám phá người chuyển phát thông qua quảng cáo của họ trên relay và lựa chọn dựa trên phí, dung lượng, hoặc phạm vi phủ

## giao tiếp

tất cả giao tiếp giữa ví và nhà vận hành, và giữa các nhà vận hành, sử dụng các nostr relay. các bản cập nhật sổ cái được xuất bản dưới dạng sự kiện bền vững mà relay lưu giữ, tạo ra một bản ghi kiểm toán vĩnh viễn. các yêu cầu và phản hồi giữa ví và nhà vận hành là các sự kiện tạm thời với TTL relay ngắn. các nhà vận hành quảng cáo điều khoản của họ dưới dạng sự kiện có thể thay thế, cho phép ví khám phá và so sánh các nhà vận hành mà không cần thư mục tập trung

kiến trúc này có nghĩa là ví không cần kết nối liên tục -- chúng có thể ngoại tuyến vô thời hạn và bắt kịp bằng cách phát lại sự kiện từ bất kỳ relay nào có chúng. các nhà vận hành có thể được liên lạc qua bất kỳ relay nào họ giám sát, và việc lựa chọn relay là quyết định triển khai, không phải ràng buộc giao thức

## dự trữ và thế chấp

dự trữ được giữ trong một utxo với số lượng lớn hơn hoặc bằng tổng nghĩa vụ của sổ cái, có thể chi tiêu bởi đa số hội đồng, với phương án dự phòng cho nhà vận hành sau một khoảng thời gian đáng kể

thế chấp là vốn riêng của nhà vận hành, được gửi và khóa trên các sổ cái thành viên hội đồng. mỗi thành viên nắm giữ một khoản tiền gửi thế chấp mà nhà vận hành cấp vốn và khóa trong một thời gian cụ thể. tổng nghĩa vụ của sổ cái được giới hạn ở mức gấp đôi khoản khóa thế chấp nhỏ nhất do bất kỳ thành viên nào nắm giữ, và thời hạn hội đồng được giới hạn ở thời gian khóa ngắn nhất. điều này đảm bảo rằng mạng lưới thế chấp luôn có đủ bảo đảm để trang trải việc chuyển giao quyền giám sát. cùng một khoản tiền gửi thế chấp có thể bảo đảm nhiều sổ cái để cải thiện hiệu quả vốn, mặc dù ví nên ưu tiên các nhà vận hành có nguồn thế chấp không trùng lặp

nghĩa vụ được thực thi khi tạo các đề nghị cấp vốn hoặc hóa đơn mới. nhà vận hành không thể tạo các đề nghị hoặc hóa đơn sẽ đẩy tổng nghĩa vụ của sổ cái vượt quá dự trữ hoặc vượt quá gấp đôi khoản khóa thế chấp nhỏ nhất, tùy theo mức nào thấp hơn

## hội đồng

các nhà vận hành yêu cầu các nhà vận hành khác tham gia hội đồng của họ bằng cách gửi và khóa thế chấp trên sổ cái của thành viên. yêu cầu bao gồm cam kết thế chấp (số lượng và thời gian khóa) và điều khoản của thành viên: lịch phí tối thiểu mà các tiền gửi trên sổ cái phải đáp ứng. mỗi thành viên phải vận hành sổ cái riêng của họ và có thể tịch thu thế chấp của nhà vận hành nếu nhà vận hành được chứng minh là không tuân thủ. các thành viên chỉ định giới hạn về lịch phí trong thời gian thành viên hội đồng của họ -- nhà vận hành không thể mở tiền gửi với phí dưới mức tối thiểu nghiêm ngặt nhất của thành viên, bảo vệ các thành viên khỏi việc thừa kế các nghĩa vụ không có lợi nhuận sau khi chuyển giao quyền giám sát

khi hội đồng được thiết lập, dự trữ được luân chuyển vào một utxo multisig mới. các thành viên đồng ký các bản cập nhật hợp lệ và tham gia khôi phục nếu nhà vận hành ký các bản cập nhật không tuân thủ. hội đồng lớn hơn tăng chi phí giao tiếp nhưng giảm rủi ro nhà vận hành, tăng khả dụng, và làm cho việc thông đồng khó khăn và tốn kém hơn. ví nên ưu tiên hội đồng lớn hơn

## răn đe kinh tế

giao thức thay thế lối thoát đơn phương bằng răn đe kinh tế. các thành viên hội đồng được khuyến khích trực tiếp hành động chống lại sự không trung thực. trong hoạt động bình thường họ kiếm được phí khiêm tốn trên thế chấp, nhưng trong trường hợp hành vi không tuân thủ có thể chứng minh được, họ có thể tịch thu toàn bộ khoản tiền gửi thế chấp của nhà vận hành trên sổ cái của họ

khi một ví nghi ngờ kiểm duyệt, nó có thể leo thang yêu cầu tới các thành viên hội đồng thông qua giao phát có xác nhận. thành viên nhúng hash yêu cầu vào sổ cái của họ với một khoản phí nhỏ, tạo ra bằng chứng được neo nhân quả. nếu nhà vận hành không xử lý yêu cầu, thành viên có cả bằng chứng và động lực kinh tế để khởi xuất tranh chấp

gian lận hóa đơn lightning theo cùng mẫu răn đe. nhà vận hành biết liệu preimage có được nhận hay không, nhưng ví thì không. tuy nhiên bất kỳ người trả nào cũng có thể cung cấp preimage cho ví. một vụ trộm được xác nhận duy nhất kích hoạt tranh chấp, tịch thu dự trữ, và tịch thu thế chấp. phần thưởng của việc ăn cắp một khoản thanh toán duy nhất là có giới hạn, nhưng rủi ro là hiện hữu, khiến việc trộm cắp qua lightning là bất hợp lý về kinh tế mặc dù không thể chứng minh chính thức được mà không có sự hợp tác của bên thứ ba

chế độ lỗi cho cả răn đe kiểm duyệt và lightning là thông đồng toàn bộ hội đồng. giao thức không thể bảo vệ chống lại một hội đồng hợp tác để ăn cắp, nhưng mạng lưới thế chấp đảm bảo rằng thông đồng tốn kém hơn những gì thu được. sự minh bạch của mạng cho phép ví và thị trường khám phá nhận diện các cấu trúc hội đồng đáng ngờ trước khi gửi tiền

## thời gian

thời gian tuyệt đối được đo dựa trên lớp cơ sở. dung sai không thể vượt quá một số xác nhận hợp lý để duy trì sự ổn định trong các cuộc tái tổ chức chuỗi

khi cần dung sai cao hơn, chúng tôi dựa vào thứ tự nhân quả. một sổ cái mật mã là một chuỗi merkle. mỗi bản cập nhật chứng minh nó được tạo ra sau tất cả các bản cập nhật trước nó, nhưng không đảm bảo gì về thông tin ngoài chuỗi. để xây dựng thứ tự phân tán, chúng tôi yêu cầu các đồng chữ ký bao gồm hash bản cập nhật mới nhất từ sổ cái của người đồng ký. hash đó sau đó được tích hợp vào hash của bản cập nhật hiện tại, trở thành một phần của chuỗi cũng như một phần của tất cả các chuỗi khác mà nhà vận hành sổ cái đồng ký, tạo ra một mạng nhân quả. điều này không thể chứng minh thời gian một cách rõ ràng, nhưng có thể chứng minh rằng các phần thông tin nhất định được tạo ra theo một thứ tự cụ thể

## bằng chứng gian lận

chúng tôi có thể chứng minh nhiều loại gian lận bằng cách phát hiện thông tin được tạo ra sai thứ tự. khi thông tin không được bao gồm bởi các hoạt động mạng bình thường, nó có thể được nhập lậu bằng cách tạo hoạt động bao gồm hash của bằng chứng. khi được tích hợp vào một bản cập nhật được nhà vận hành ký, bằng chứng được tiết lộ là đã được tạo ra tại một vị trí không tuân thủ trong thứ tự:

- một nhà vận hành, đã đề nghị ghi có cho một tiền gửi với tiền gửi trên chuỗi tới một địa chỉ cụ thể, ký một bản cập nhật sổ cái không chứa khoản ghi có thích hợp, nhưng chứa một chuỗi tiết lộ hash khối vượt quá số xác nhận cho phép trước khi ghi có

- một nhà vận hành, đã tạo một hóa đơn lightning thay mặt tiền gửi, ký một bản cập nhật sổ cái chưa ghi có cho tiền gửi mặc dù preimage đã được tiết lộ trong chuỗi

- một đồng chữ ký tuyên bố hash sổ cái hiện tại là hash trước hash sau của chính họ trong chuỗi

- một thành viên hội đồng của sổ cái bị tranh chấp đã hoạt động nhưng không hành động phù hợp với bằng chứng gian lận trong một số khối

- ký hoặc đồng ký các bản cập nhật sổ cái không tuân thủ

một bằng chứng gian lận bao gồm bằng chứng và một chuỗi nhân quả kết nối hash được nhúng với sổ cái của nhà vận hành bị cáo buộc. chuỗi là một chuỗi các bản cập nhật được đồng ký, mỗi bản bao gồm một member_ledger_hash từ sổ cái của liên kết trước. người xác minh duyệt chuỗi mà không cần tìm kiếm, xác nhận mỗi liên kết là một bản cập nhật đã ký, và rằng hash bằng chứng khớp với dữ liệu được nhúng

## khôi phục

khi một sổ cái trở nên không khả dụng hoặc không tuân thủ, các thành viên hội đồng có thể tạo phiên bản tiếp tục của sổ cái từ bản cập nhật tuân thủ cuối cùng. họ phải thiết lập hội đồng mới và cung cấp chứng nhận thế chấp. các thành viên sau đó phải phối hợp để chi tiêu đầu ra dự trữ trước đó cho một cuộc xổ số của các chuỗi tiếp theo tiềm năng. người thắng cuộc xổ số này thêm bản cập nhật tiếp nhận vào chuỗi của họ, và những người khác thêm bản nhường quyền. ví tiếp tục địa chỉ đến cùng sổ cái, chỉ chấp nhận các phản hồi được hội đồng đồng ký. định kỳ, và khi không có phản hồi nào có đồng chữ ký mong đợi, ví nên truy vấn mạng và phát lại các bản cập nhật sổ cái để nhận biết thay đổi trong quyền giám sát

khi sự không tuân thủ có vẻ là vô tình (vd, một sổ cái đã trở nên không khả dụng trong một số khối nhất định) việc thay đổi quyền giám sát phải tôn trọng: chỉ số lượng dự trữ cần thiết để trang trải nghĩa vụ của sổ cái được gửi đến cuộc xổ số, và phần còn lại gửi về khóa công khai của nhà vận hành. quyền kiểm soát thế chấp không bị ảnh hưởng

khi có bằng chứng không tuân thủ, số tiền vượt quá dự trữ cần thiết được chia đều cho các thành viên hội đồng, và thế chấp giữ trên sổ cái thành viên được phép tịch thu

## sức khỏe mạng

một cuộc tấn công đơn giản là hình thành các nhóm nhà vận hành thông đồng. sau khi xây dựng nghĩa vụ đáng kể trên các sổ cái của họ, họ phối hợp rút tiền, ăn cắp tiền vượt quá thế chấp bị mất. mạng có thể phòng thủ chống lại điều này, ngoại trừ ở những khu vực mà giá trị nội bộ vượt quá thế chấp kết nối nó với mạng không thông đồng. tỷ lệ thế chấp cao hơn và hội đồng lớn hơn, đa dạng hơn giảm khả năng hình thành các túi này, nhưng chúng có thể hình thành có chủ đích và chúng tôi không thể kỳ vọng mọi ví đánh giá toàn bộ mạng. thay vào đó các thị trường khám phá nên công bố các chỉ số trách nhiệm của nhà vận hành dựa trên phân tích đồ thị như các thuật toán thu thập giải thưởng

## kết luận

chúng tôi đề xuất một mạng lưới thế chấp yêu cầu thông đồng để ăn cắp, nhưng thông đồng làm tăng thế chấp gặp rủi ro nhanh hơn giá trị có thể bị ăn cắp. chúng tôi sử dụng mạng này để bảo mật các sổ cái mật mã được bảo đảm bởi dự trữ đầy đủ. các sổ cái này phục vụ tài khoản thay mặt cho các ví ngoại tuyến để đổi lấy phí được thương lượng trước. các nguyên thủy sổ cái hỗ trợ các điều kiện chi tiêu miniscript đủ cho các hợp đồng thông minh cơ bản. mạng mở rộng gần tuyến tính, cho phép một mạng lớn cung cấp hàng tỷ ví và khối lượng giao dịch vượt quá các mạng thanh toán truyền thống
