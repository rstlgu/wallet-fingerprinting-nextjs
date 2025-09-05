import WalletAnalyzer from '@/components/WalletAnalyzer';

/**
 * The main page component that renders the WalletAnalyzer component.
 *
 * @returns {JSX.Element} The rendered WalletAnalyzer component.
 */
export default function Page() {
    return (
        <div className="min-h-screen bg-background">
            <WalletAnalyzer />
        </div>
    );
}
