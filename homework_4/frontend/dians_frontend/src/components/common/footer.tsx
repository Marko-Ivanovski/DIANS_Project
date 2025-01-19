import Link from "next/link";
import Image from "next/image";

const Footer = () => {
  return (
    <footer className="footer mt-auto">
      <div className="container">
        <div className="footer-left">
          <Link href="/">
            <Image src="/Images/Logo.png" alt="Macedonian Stock Exchange Logo" width={100} height={50} />
          </Link>
          <p>
            Stay informed with the latest stock trends and market analysis. Our platform provides real-time updates and historical data to empower your investment decisions.
          </p>
          {/*<div className="buttons">*/}
          {/*  <Link href="/login"><button className="login-btn">Log In</button></Link>*/}
          {/*  <Link href="/signup"><button className="signup-btn">Sign Up</button></Link>*/}
          {/*</div>*/}
        </div>
        <div className="footer-right">
          <div className="list-container">
            <div className="list-title">Quick Links</div>
            <ul>
              <li><Link href="/">Home</Link></li>
              <li><Link href="/about">About Us</Link></li>
              <li><Link href="/my-stocks">My Stocks</Link></li>
            </ul>
          </div>
          <div className="list-container">
            <div className="list-title">Get In Touch</div>
            <ul>
              <li>Skopje, Macedonia</li>
              <li>johndoe@example.com</li>
              <li>+389 12 34 56</li>
            </ul>
          </div>
          <div className="list-container">
            <div className="list-title">Social Media</div>
            <ul>
              <li>Facebook</li>
              <li>Twitter</li>
              <li>LinkedIn</li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;