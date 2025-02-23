import Mobelix from "./Mobelix.png";
import Anhoch from "./Anhoch.png";
import Neptun from "./Neptun.png";
import Setec from "./Setec.png";
import Telekom from "./Telekom.png";

export default class Images {
    static Mobelix = Mobelix;
    static Anhoch = Anhoch;
    static Neptun = Neptun;
    static Setec = Setec;
    static Telekom = Telekom;
    static getVendorImage = (vendor) => {
        switch (vendor) {
            case "Mobelix":
                return Images.Mobelix;
            case "Anhoch":
                return Images.Anhoch;
            case "Neptun":
                return Images.Neptun;
            case "Telekom":
                return Images.Telekom;
            case "Setec":
                return Images.Setec;
            default:
                return "";
        }
    };
}
