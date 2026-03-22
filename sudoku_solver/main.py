import sys

def main():

    print("=" * 50)
    print("    🧩 Sudoku Solver - DP + Backtracking")
    print("=" * 50)
    print("\nStarting application...")
    print("- Uses Dynamic Programming for constraint caching")
    print("- Optimized with Minimum Remaining Values heuristic")
    print("- Real-time solving visualization")
    print("\n" + "=" * 50)
    
    try:

        from gui import create_app
        
        app = create_app()
        print("\n✅ Application started successfully!")
        print("   Close the window to exit.\n")
     
        app.run()
        
    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print("   Make sure all project files are in the same directory.")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    
    print("\n👋 Thanks for using Sudoku Solver!")
    print("=" * 50)


if __name__ == "__main__":
    main()
